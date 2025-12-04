// -------------------------------------------------------------------------------------------------
//  Copyright (C) 2015-2025 Nautech Systems Pty Ltd. All rights reserved.
//  https://nautechsystems.io
//
//  Licensed under the GNU Lesser General Public License Version 3.0 (the "License");
//  You may not use this file except in compliance with the License.
//  You may obtain a copy of the License at https://www.gnu.org/licenses/lgpl-3.0.en.html
//
//  Unless required by applicable law or agreed to in writing, software
//  distributed under the License is distributed on an "AS IS" BASIS,
//  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//  See the License for the specific language governing permissions and
//  limitations under the License.
// -------------------------------------------------------------------------------------------------

//! Python enum bindings for the Lys adapter.

use pyo3::prelude::*;
use crate::common::enums::{LysExecutionType, LysEventType, LysTransport};

#[pyclass(name = "LysExecutionType")]
#[derive(Clone)]
pub struct PyLysExecutionType {
    #[pyo3(get)]
    pub value: String,
}

#[pymethods]
impl PyLysExecutionType {
    #[classattr]
    const PUMP_FUN: &'static str = "PUMP_FUN";

    #[classattr]
    const RAYDIUM: &'static str = "RAYDIUM";

    #[classattr]
    const JUPITER: &'static str = "JUPITER";

    #[classattr]
    const CUSTOM: &'static str = "CUSTOM";
}

#[pyclass(name = "LysEventType")]
#[derive(Clone)]
pub struct PyLysEventType {
    #[pyo3(get)]
    pub value: String,
}

#[pymethods]
impl PyLysEventType {
    #[classattr]
    const BUY: &'static str = "BUY";

    #[classattr]
    const SELL: &'static str = "SELL";
}

#[pyclass(name = "LysTransport")]
#[derive(Clone)]
pub struct PyLysTransport {
    #[pyo3(get)]
    pub value: String,
}

#[pymethods]
impl PyLysTransport {
    #[classattr]
    const STANDARD: &'static str = "STANDARD";

    #[classattr]
    const NONCE: &'static str = "NONCE";

    #[classattr]
    const PRIORITY: &'static str = "PRIORITY";
}
