<?php

declare(strict_types=1);

/**
 * Recovery Error Exception
 *
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * @package MokoStandards\Enterprise
 * @version 04.00.03
 * @author MokoStandards Team
 * @license GPL-3.0-or-later
 */

namespace MokoStandards\Enterprise;

use RuntimeException;

/**
 * Exception raised when recovery operations fail.
 */
class RecoveryError extends RuntimeException
{
}
