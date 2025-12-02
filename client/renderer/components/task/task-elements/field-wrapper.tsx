import React, { PropsWithChildren } from "react";
import { Stack, SxProps, Theme } from "@mui/material";
import { FIELD_SPACING } from "./field-sizes";

interface FieldWrapperProps {
  /** Custom margin top override */
  mt?: number;
  /** Custom margin left override */
  ml?: number;
  /** Additional sx props */
  sx?: SxProps<Theme>;
  /** ARIA label for accessibility */
  ariaLabel?: string;
}

/**
 * Consistent wrapper for form field components.
 *
 * Provides standardized spacing and layout for all field types,
 * ensuring visual consistency across task interfaces.
 */
export const FieldWrapper: React.FC<PropsWithChildren<FieldWrapperProps>> = ({
  children,
  mt = FIELD_SPACING.marginTop,
  ml = FIELD_SPACING.marginLeft,
  sx,
  ariaLabel,
}) => (
  <Stack
    direction="row"
    sx={{
      mt,
      ml,
      alignItems: "flex-start",
      ...sx,
    }}
    role="group"
    aria-label={ariaLabel}
  >
    {children}
  </Stack>
);

export default FieldWrapper;
