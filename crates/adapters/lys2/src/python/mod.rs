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

//! Python bindings for the Lys adapter.

use pyo3::prelude::*;

pub mod enums;
pub mod websocket;
pub mod zmq;

/// Loaded as `nautilus_lys2`
#[pymodule]
pub fn nautilus_lys2(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    // Register enums
    m.add_class::<enums::PyLysExecutionType>()?;
    m.add_class::<enums::PyLysEventType>()?;
    m.add_class::<enums::PyLysTransport>()?;

    // Register clients
    m.add_class::<zmq::PyLysZmqClient>()?;
    m.add_class::<websocket::PyLysWebSocketClient>()?;

    Ok(())
}
