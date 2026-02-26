<?php
/**
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * This file is part of a Moko Consulting project.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * FILE INFORMATION
 * DEFGROUP: MokoStandards.Enterprise
 * INGROUP: MokoStandards
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: /src/Enterprise/SynchronizationException.php
 * VERSION: 05.00.00
 * BRIEF: Custom exception for repository synchronization errors
 */

declare(strict_types=1);

namespace MokoStandards\Enterprise;

use RuntimeException;

/**
 * Exception thrown when repository synchronization fails or is not implemented
 */
class SynchronizationNotImplementedException extends RuntimeException
{
    /**
     * Create exception for unimplemented synchronization logic
     * 
     * @return self
     */
    public static function create(): self
    {
        return new self(
            "Repository synchronization logic is not implemented. " .
            "The processRepository() method contains only placeholder code. " .
            "Actual file synchronization, PR creation, and merge handling must be implemented."
        );
    }
}
