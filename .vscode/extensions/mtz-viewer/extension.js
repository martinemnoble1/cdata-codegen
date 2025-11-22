const vscode = require('vscode');
const { spawn } = require('child_process');
const path = require('path');

/**
 * MTZ File Viewer Extension for VS Code
 *
 * Displays MTZ file metadata using the mtz_preview.py script
 */

function activate(context) {
    let disposable = vscode.commands.registerCommand('mtzViewer.preview', async (uri) => {
        // Get the MTZ file path
        let mtzPath;
        if (uri && uri.fsPath) {
            mtzPath = uri.fsPath;
        } else {
            // If called from command palette, ask for file
            const editor = vscode.window.activeTextEditor;
            if (editor) {
                mtzPath = editor.document.uri.fsPath;
            } else {
                vscode.window.showErrorMessage('No MTZ file selected');
                return;
            }
        }

        if (!mtzPath.endsWith('.mtz')) {
            vscode.window.showErrorMessage('Selected file is not an MTZ file');
            return;
        }

        // Get the Python script path
        const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
        if (!workspaceFolder) {
            vscode.window.showErrorMessage('No workspace folder found');
            return;
        }

        const scriptPath = path.join(
            workspaceFolder.uri.fsPath,
            'tools',
            'mtz_preview.py'
        );

        // Get Python path
        const pythonPath = await getPythonPath(workspaceFolder.uri.fsPath);

        // Create and show webview panel
        const panel = vscode.window.createWebviewPanel(
            'mtzPreview',
            `MTZ: ${path.basename(mtzPath)}`,
            vscode.ViewColumn.One,
            {
                enableScripts: false,
                retainContextWhenHidden: true
            }
        );

        panel.webview.html = getLoadingHtml();

        // Run preview script
        runPreviewScript(pythonPath, scriptPath, mtzPath, panel);
    });

    context.subscriptions.push(disposable);
}

async function getPythonPath(workspaceRoot) {
    // Check for .venv/bin/python
    const venvPython = path.join(workspaceRoot, '.venv', 'bin', 'python');
    try {
        const fs = require('fs');
        if (fs.existsSync(venvPython)) {
            return venvPython;
        }
    } catch (e) {
        // Fall through to system python
    }

    // Use system python3
    return 'python3';
}

function runPreviewScript(pythonPath, scriptPath, mtzPath, panel) {
    const process = spawn(pythonPath, [scriptPath, mtzPath]);
    let stdout = '';
    let stderr = '';

    process.stdout.on('data', (data) => {
        stdout += data.toString();
    });

    process.stderr.on('data', (data) => {
        stderr += data.toString();
    });

    process.on('close', (code) => {
        if (code !== 0) {
            panel.webview.html = getErrorHtml(
                `Failed to parse MTZ file (exit code ${code}):\n${stderr}`
            );
            return;
        }

        // Convert markdown to HTML
        panel.webview.html = getPreviewHtml(stdout, mtzPath);
    });

    process.on('error', (err) => {
        panel.webview.html = getErrorHtml(
            `Failed to run preview script: ${err.message}`
        );
    });
}

function getLoadingHtml() {
    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MTZ Preview</title>
    <style>
        body {
            padding: 20px;
            font-family: var(--vscode-font-family);
            color: var(--vscode-foreground);
            background-color: var(--vscode-editor-background);
        }
        .loading {
            text-align: center;
            padding: 40px;
            color: var(--vscode-descriptionForeground);
        }
    </style>
</head>
<body>
    <div class="loading">
        <p>Loading MTZ file preview...</p>
    </div>
</body>
</html>`;
}

function getErrorHtml(error) {
    const escapedError = escapeHtml(error);
    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MTZ Preview Error</title>
    <style>
        body {
            padding: 20px;
            font-family: var(--vscode-font-family);
            color: var(--vscode-foreground);
            background-color: var(--vscode-editor-background);
        }
        .error {
            color: var(--vscode-errorForeground);
            background-color: var(--vscode-inputValidation-errorBackground);
            border: 1px solid var(--vscode-inputValidation-errorBorder);
            padding: 16px;
            border-radius: 4px;
        }
        pre {
            white-space: pre-wrap;
            word-wrap: break-word;
        }
    </style>
</head>
<body>
    <div class="error">
        <h2>Error</h2>
        <pre>${escapedError}</pre>
    </div>
</body>
</html>`;
}

function getPreviewHtml(markdownContent, mtzPath) {
    // Convert markdown to HTML (simple conversion)
    const html = markdownToHtml(markdownContent);

    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MTZ Preview</title>
    <style>
        body {
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
            font-family: var(--vscode-font-family);
            color: var(--vscode-foreground);
            background-color: var(--vscode-editor-background);
            line-height: 1.6;
        }
        h1, h2, h3 {
            color: var(--vscode-textLink-foreground);
            border-bottom: 1px solid var(--vscode-panel-border);
            padding-bottom: 8px;
            margin-top: 24px;
        }
        h1 {
            font-size: 1.8em;
        }
        h2 {
            font-size: 1.4em;
            margin-top: 32px;
        }
        h3 {
            font-size: 1.2em;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 16px 0;
            font-size: 0.9em;
        }
        th {
            background-color: var(--vscode-editor-selectionBackground);
            color: var(--vscode-editor-foreground);
            font-weight: bold;
            padding: 8px 12px;
            text-align: left;
            border: 1px solid var(--vscode-panel-border);
        }
        td {
            padding: 6px 12px;
            border: 1px solid var(--vscode-panel-border);
        }
        tr:nth-child(even) {
            background-color: var(--vscode-list-hoverBackground);
        }
        code {
            background-color: var(--vscode-textCodeBlock-background);
            padding: 2px 6px;
            border-radius: 3px;
            font-family: var(--vscode-editor-font-family);
            font-size: 0.9em;
        }
        ul {
            padding-left: 24px;
        }
        li {
            margin: 4px 0;
        }
        strong {
            color: var(--vscode-textPreformat-foreground);
        }
        .file-path {
            font-size: 0.85em;
            color: var(--vscode-descriptionForeground);
            font-family: monospace;
        }
    </style>
</head>
<body>
    ${html}
</body>
</html>`;
}

function markdownToHtml(markdown) {
    let html = markdown;

    // Convert headers
    html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
    html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
    html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');

    // Convert bold
    html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

    // Convert inline code
    html = html.replace(/`(.+?)`/g, '<code>$1</code>');

    // Convert lists
    html = html.replace(/^- (.+)$/gm, '<li>$1</li>');
    html = html.replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>');

    // Convert tables
    html = html.replace(/\|(.+)\|\n\|[-:| ]+\|\n((?:\|.+\|\n?)+)/g, (match, header, rows) => {
        const headerCells = header.split('|').filter(c => c.trim()).map(c =>
            `<th>${c.trim()}</th>`
        ).join('');
        const rowHtml = rows.trim().split('\n').map(row => {
            const cells = row.split('|').filter(c => c.trim()).map(c =>
                `<td>${c.trim()}</td>`
            ).join('');
            return `<tr>${cells}</tr>`;
        }).join('\n');
        return `<table><thead><tr>${headerCells}</tr></thead><tbody>${rowHtml}</tbody></table>`;
    });

    // Convert line breaks
    html = html.replace(/\n\n/g, '<br><br>');
    html = html.replace(/\n/g, ' ');

    return html;
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};
