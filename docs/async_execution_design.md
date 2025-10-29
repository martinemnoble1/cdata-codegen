# Async Execution Design: Qt-free Implementation

## Overview

This document describes how to replace Qt's QProcess-based async execution with a pure Python asyncio-based system that works with our modern signal/slot implementation.

## Current Qt-Based Pattern

### How It Works

```python
class prosmart_refmac(CPluginScript):
    ASYNCHRONOUS = True

    def executeProsmartProtein(self):
        # Create sub-plugin
        self.prosmart_protein = self.makePluginObject('prosmart')

        # Configure parameters
        self.prosmart_protein.container.inputData.TARGET_MODEL = self.container.inputData.XYZIN

        # Connect finished signal to handler
        self.connectSignal(self.prosmart_protein, 'finished', self.prosmartProteinFinished)

        # Set async mode
        self.prosmart_protein.waitForFinished = -1

        # Start process (non-blocking)
        self.prosmart_protein.process()

    @QtCore.Slot(dict)
    def prosmartProteinFinished(self, statusDict):
        """Called when prosmart finishes."""
        status = statusDict['finishStatus']
        if status == CPluginScript.FAILED:
            self.reportStatus(status)
            return

        # Continue with next step...
        self.executeRefmac()
```

### Key Components

1. **CPluginScript**:
   - Has `finished = QtCore.Signal(dict)` attribute
   - When async (`ASYNCHRONOUS = True`), uses `QProcess` to run subprocess
   - When process completes, emits `finished` signal with status dict

2. **CProcessManager**:
   - Manages `QProcess` instances
   - Connects `QProcess.finished` to `handleFinish()`
   - `handleFinish()` calls registered handler, which emits plugin's `finished` signal

3. **Signal Connection**:
   - `connectSignal(origin, 'finished', handler)` → `origin.finished.connect(handler)`
   - Qt automatically calls handler when signal emitted

## Qt-Free Design

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   CPluginScript                         │
│  - finished: Signal[dict]                               │
│  - process(): Start execution                           │
│  - _run_async(): asyncio subprocess execution           │
│  - connectSignal(): Connect to our Signal               │
└───────────────────┬─────────────────────────────────────┘
                    │
                    │ uses
                    ▼
┌─────────────────────────────────────────────────────────┐
│              AsyncProcessManager                         │
│  - startProcess(): Launch subprocess with asyncio       │
│  - _monitor_process(): Wait for completion              │
│  - _handle_finish(): Call handler when done             │
└───────────────────┬─────────────────────────────────────┘
                    │
                    │ uses
                    ▼
┌─────────────────────────────────────────────────────────┐
│              signal_system.Signal                        │
│  - connect(slot): Register callback                     │
│  - emit(*args): Call all connected slots                │
│  - emit_async(*args): Async version                     │
└─────────────────────────────────────────────────────────┘
```

### Key Changes

1. **Replace QProcess with asyncio.subprocess**:
   ```python
   # Old (Qt)
   p = QtCore.QProcess()
   p.start(command, args)
   p.finished.connect(handler)

   # New (asyncio)
   process = await asyncio.create_subprocess_exec(
       command, *args,
       stdout=asyncio.subprocess.PIPE,
       stderr=asyncio.subprocess.PIPE
   )
   returncode = await process.wait()
   ```

2. **Replace QSignal with our Signal**:
   ```python
   # Old (Qt)
   finished = QtCore.Signal(dict)

   # New (our system)
   from core.base_object.signal_system import Signal
   finished = Signal[dict]()
   ```

3. **Update connectSignal**:
   ```python
   def connectSignal(self, origin, signal_name, handler):
       """Connect a signal to a handler."""
       if signal_name == 'finished' and hasattr(origin, 'finished'):
           origin.finished.connect(handler, weak=False)
       else:
           raise ValueError(f"Unknown signal: {signal_name}")
   ```

### Implementation Details

#### 1. AsyncProcessManager

```python
class AsyncProcessManager:
    """
    Manages async subprocess execution using asyncio.

    Replaces Qt's QProcess-based CProcessManager.
    """

    def __init__(self):
        self.processes = {}  # pid -> process info
        self._next_pid = 1000
        self._lock = asyncio.Lock()
        self._executor = ThreadPoolExecutor(max_workers=4)

    async def startProcess(
        self,
        command: str,
        args: List[str] = None,
        inputFile: str = None,
        logFile: str = None,
        cwd: str = None,
        env: Dict[str, str] = None,
        handler: Callable = None,
        timeout: int = None
    ) -> int:
        """
        Start an async subprocess.

        Returns:
            Process ID (int)
        """
        async with self._lock:
            pid = self._next_pid
            self._next_pid += 1

        # Store process info
        self.processes[pid] = {
            'command': command,
            'args': args or [],
            'logFile': logFile,
            'cwd': cwd,
            'handler': handler,
            'startTime': time.time(),
            'status': 'running'
        }

        # Launch monitoring task
        asyncio.create_task(self._monitor_process(pid, command, args, inputFile, logFile, cwd, env, timeout))

        return pid

    async def _monitor_process(self, pid, command, args, inputFile, logFile, cwd, env, timeout):
        """Monitor subprocess until completion."""
        try:
            # Prepare stdin
            stdin = None
            if inputFile:
                stdin = asyncio.subprocess.PIPE

            # Prepare stdout/stderr
            stdout_dest = asyncio.subprocess.PIPE
            stderr_dest = asyncio.subprocess.PIPE

            # Launch subprocess
            process = await asyncio.create_subprocess_exec(
                command,
                *(args or []),
                stdin=stdin,
                stdout=stdout_dest,
                stderr=stderr_dest,
                cwd=cwd,
                env=env
            )

            # Send input file if needed
            if inputFile:
                with open(inputFile, 'rb') as f:
                    input_data = f.read()
                await process.stdin.write(input_data)
                await process.stdin.drain()
                process.stdin.close()

            # Wait for completion (with timeout)
            try:
                if timeout and timeout > 0:
                    stdout, stderr = await asyncio.wait_for(
                        process.communicate(),
                        timeout=timeout / 1000.0  # Convert ms to seconds
                    )
                else:
                    stdout, stderr = await process.communicate()
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                self.processes[pid]['status'] = 'timeout'
                self.processes[pid]['exitCode'] = -1
                await self._handle_finish(pid, -1, 1)
                return

            # Save output to log files
            if logFile:
                with open(logFile, 'wb') as f:
                    f.write(stdout)

                # Save stderr to separate file
                err_file = logFile.replace('.log', '_err.txt')
                if stderr:
                    with open(err_file, 'wb') as f:
                        f.write(stderr)

            # Update process info
            self.processes[pid]['exitCode'] = process.returncode
            self.processes[pid]['exitStatus'] = 0 if process.returncode == 0 else 1
            self.processes[pid]['finishTime'] = time.time()
            self.processes[pid]['status'] = 'finished'

            # Call completion handler
            await self._handle_finish(pid, process.returncode, 0 if process.returncode == 0 else 1)

        except Exception as e:
            logger.error(f"Error in process {pid}: {e}")
            self.processes[pid]['status'] = 'error'
            self.processes[pid]['error'] = str(e)
            await self._handle_finish(pid, -1, 1)

    async def _handle_finish(self, pid, exitCode, exitStatus):
        """Handle process completion."""
        info = self.processes.get(pid, {})
        handler = info.get('handler')

        if handler:
            # Call the handler (which is [callback, kwargs] format)
            if isinstance(handler, list) and len(handler) >= 1:
                callback = handler[0]
                kwargs = handler[1] if len(handler) > 1 else {}

                # Call with pid as argument
                if asyncio.iscoroutinefunction(callback):
                    await callback(pid, **kwargs)
                else:
                    # Run sync function in executor
                    loop = asyncio.get_event_loop()
                    await loop.run_in_executor(self._executor, lambda: callback(pid, **kwargs))

    def getJobData(self, pid, attribute='exitStatus'):
        """Get data about a process."""
        return self.processes.get(pid, {}).get(attribute)
```

#### 2. Updated CPluginScript

```python
class CPluginScript:
    """
    Base class for plugin scripts with async support.
    """

    # Class attributes
    ASYNCHRONOUS = False

    def __init__(self, parent=None, name=None, **kwargs):
        super().__init__(parent=parent, name=name)

        # Use our Signal class instead of QtCore.Signal
        from core.base_object.signal_system import Signal
        self.finished = Signal[dict](name=f'{name}_finished')

        self._runningProcessId = None
        self._ifAsync = self.ASYNCHRONOUS

    def connectSignal(self, origin, signal_name: str, handler):
        """
        Connect a signal from origin object to a handler.

        Compatible with Qt-based code but uses our Signal system.
        """
        if signal_name == 'finished' and hasattr(origin, 'finished'):
            # Connect to our Signal (not Qt)
            origin.finished.connect(handler, weak=False)
        else:
            raise ValueError(f"Unknown signal '{signal_name}' on {origin}")

    def process(self, **kwargs):
        """
        Main entry point - check inputs and start process.
        """
        # ... input checking ...

        # Start process
        if self._ifAsync:
            # Run async
            return self._start_async_process(**kwargs)
        else:
            # Run sync
            return self._start_sync_process(**kwargs)

    def _start_async_process(self, **kwargs):
        """Start process asynchronously using asyncio."""
        # Get or create event loop
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            # No loop running, create one
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        # Schedule async execution
        task = asyncio.create_task(self._run_async_process(**kwargs))

        # Return immediately (non-blocking)
        return CPluginScript.SUCCEEDED

    async def _run_async_process(self, **kwargs):
        """Async process execution."""
        # Get process manager
        from core import CCP4Modules
        pm = CCP4Modules.ASYNC_PROCESSMANAGER()

        # Start subprocess
        handler = [self.postProcess, {}]

        self._runningProcessId = await pm.startProcess(
            command=self.command,
            args=self.commandLine,
            inputFile=self.makeFileName('COM') if self.commandScript else None,
            logFile=self.makeFileName('LOG'),
            cwd=self.workDirectory,
            handler=handler,
            timeout=self._timeout
        )

    def postProcess(self, processId):
        """Called when process finishes."""
        # Check exit status
        exitStatus = self.getJobData(processId, 'exitStatus')
        exitCode = self.getJobData(processId, 'exitCode')

        if exitStatus != 0 or exitCode != 0:
            finishStatus = CPluginScript.FAILED
        else:
            finishStatus = CPluginScript.SUCCEEDED

        # Process output files
        try:
            self.processOutputFiles()
        except Exception as e:
            finishStatus = CPluginScript.FAILED

        # Emit finished signal
        status_dict = {
            'jobId': self._dbJobId,
            'pid': processId,
            'finishStatus': finishStatus
        }

        self.finished.emit(status_dict)

        return finishStatus
```

#### 3. Event Loop Management

Since asyncio requires an event loop, we need to manage it carefully:

```python
# In core/CCP4Modules.py

def ASYNC_PROCESSMANAGER():
    """Get the singleton async process manager."""
    from core.async_process_manager import AsyncProcessManager

    if not hasattr(ASYNC_PROCESSMANAGER, '_instance'):
        ASYNC_PROCESSMANAGER._instance = AsyncProcessManager()

        # Ensure event loop is running
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            # Start background event loop in thread
            loop = asyncio.new_event_loop()
            def run_loop():
                asyncio.set_event_loop(loop)
                loop.run_forever()

            import threading
            thread = threading.Thread(target=run_loop, daemon=True)
            thread.start()
            ASYNC_PROCESSMANAGER._loop = loop

    return ASYNC_PROCESSMANAGER._instance
```

## Migration Path

### Phase 1: Parallel Implementation
- Keep Qt-based system working
- Add new async system alongside
- Use environment variable or config to choose: `USE_ASYNC_PROCESS_MANAGER=True`

### Phase 2: Testing
- Run existing async plugins with new system
- Verify `prosmart_refmac`, `coot_rebuild`, `xia2_dials` all work
- Check signal emission and handler calls

### Phase 3: Full Migration
- Switch default to new system
- Remove Qt dependencies from CProcessManager
- Update all plugins to use new patterns

## Benefits

1. **No Qt Dependency**: Pure Python asyncio
2. **Better Performance**: Native async/await instead of Qt event loop
3. **Modern Python**: Uses typing, dataclasses, etc.
4. **Easier Testing**: Can test async code with pytest-asyncio
5. **Cross-platform**: asyncio works everywhere without Qt
6. **Signal System**: Already integrated with our Signal class

## Example Usage

```python
from core.CCP4PluginScript import CPluginScript
from core.base_object.signal_system import Slot

class MyPipeline(CPluginScript):
    ASYNCHRONOUS = True

    def process(self):
        # Start first subprocess
        self.refmac1 = self.makePluginObject('refmac')
        self.refmac1.container.inputData.XYZIN = self.container.inputData.XYZIN

        # Connect signal
        self.connectSignal(self.refmac1, 'finished', self.refmac1Finished)

        # Start async
        self.refmac1.process()

        return CPluginScript.SUCCEEDED

    @Slot(dict)
    def refmac1Finished(self, statusDict):
        """Called when first refmac finishes."""
        if statusDict['finishStatus'] != CPluginScript.SUCCEEDED:
            self.reportStatus(CPluginScript.FAILED)
            return

        # Start second subprocess
        self.refmac2 = self.makePluginObject('refmac')
        self.refmac2.container.inputData.XYZIN = self.refmac1.container.outputData.XYZOUT

        self.connectSignal(self.refmac2, 'finished', self.refmac2Finished)
        self.refmac2.process()

    @Slot(dict)
    def refmac2Finished(self, statusDict):
        """Called when second refmac finishes."""
        # Final step
        self.reportStatus(statusDict['finishStatus'])
```

## Testing

```python
import pytest
import asyncio
from core.async_process_manager import AsyncProcessManager

@pytest.mark.asyncio
async def test_async_subprocess():
    """Test async subprocess execution."""
    pm = AsyncProcessManager()

    # Track completion
    completed = asyncio.Event()
    result_data = {}

    def handler(pid):
        result_data['pid'] = pid
        result_data['exitCode'] = pm.getJobData(pid, 'exitCode')
        completed.set()

    # Start process
    pid = await pm.startProcess(
        command='echo',
        args=['hello world'],
        handler=[handler, {}]
    )

    # Wait for completion
    await asyncio.wait_for(completed.wait(), timeout=5.0)

    # Verify
    assert result_data['exitCode'] == 0
    assert pm.getJobData(pid, 'status') == 'finished'

@pytest.mark.asyncio
async def test_plugin_async_execution():
    """Test plugin with async execution."""
    from tests.mocks import MockPlugin

    plugin = MockPlugin(name='test_async')
    plugin.ASYNCHRONOUS = True

    # Track finish
    finished_status = None

    @Slot(dict)
    def on_finished(status_dict):
        nonlocal finished_status
        finished_status = status_dict['finishStatus']

    plugin.connectSignal(plugin, 'finished', on_finished)

    # Start
    plugin.process()

    # Wait for completion (max 10 seconds)
    for _ in range(100):
        if finished_status is not None:
            break
        await asyncio.sleep(0.1)

    assert finished_status == CPluginScript.SUCCEEDED
```

## Open Questions

1. **Event Loop Management**: Should we run one global event loop in a background thread, or create new loops per plugin?
   - **Recommendation**: One global loop in background thread (simpler)

2. **Backwards Compatibility**: How to support plugins that still expect Qt?
   - **Recommendation**: Check `if QT()` and use appropriate system

3. **Signal Emission**: Should we use `emit()` or `emit_async()`?
   - **Recommendation**: Use `emit()` from background event loop thread (works with sync handlers)

4. **Process Limits**: How to limit concurrent processes (like `MAXNJOBS = 4`)?
   - **Recommendation**: Add semaphore to AsyncProcessManager

## Next Steps

1. Implement `AsyncProcessManager` class
2. Update `CPluginScript` with async support
3. Create compatibility layer for existing plugins
4. Write comprehensive tests
5. Test with prosmart_refmac pipeline
6. Document migration guide for plugin developers
