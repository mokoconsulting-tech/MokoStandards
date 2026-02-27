<?php
/**
 * MokoStandards Common Functions
 * 
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 * 
 * SPDX-License-Identifier: GPL-3.0-or-later
 * 
 * This file provides global helper functions for MokoStandards.
 * 
 * @package MokoStandards
 * @version 04.00.03
 */

declare(strict_types=1);

if (!function_exists('mokostandards_version')) {
    /**
     * Get the MokoStandards version
     *
     * @return string Version number
     */
    function mokostandards_version(): string
    {
        return '04.00.03';
    }
}

if (!function_exists('mokostandards_root_dir')) {
    /**
     * Get the MokoStandards root directory
     *
     * @return string Root directory path
     */
    function mokostandards_root_dir(): string
    {
        return dirname(__DIR__);
    }
}
