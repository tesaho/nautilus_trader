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

//! Python bindings for Lys WebSocket client.

use pyo3::prelude::*;
use futures::StreamExt;
use tokio_tungstenite::tungstenite::Message;
use crate::websocket::LysWebSocketClient;

fn to_pyerr(err: impl std::fmt::Display) -> PyErr {
    pyo3::exceptions::PyRuntimeError::new_err(err.to_string())
}

/// Python wrapper for Lys WebSocket client
#[pyclass(name = "LysWebSocketClient")]
pub struct PyLysWebSocketClient {
    client: LysWebSocketClient,
}

#[pymethods]
impl PyLysWebSocketClient {
    /// Create a new Lys WebSocket client
    ///
    /// Parameters
    /// ----------
    /// base_url : str
    ///     WebSocket base URL
    /// api_key : str
    ///     Lys API key
    #[new]
    fn py_new(base_url: String, api_key: String) -> PyResult<Self> {
        let client = LysWebSocketClient::new(base_url, api_key);
        Ok(Self { client })
    }

    /// Connect to the WebSocket server
    #[pyo3(name = "connect")]
    fn py_connect<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyAny>> {
        let client = self.client.clone();
        pyo3_async_runtimes::tokio::future_into_py(py, async move {
            client.connect().await.map_err(to_pyerr)?;
            Ok(())
        })
    }

    /// Subscribe to transaction stream
    #[pyo3(name = "subscribe_transactions")]
    fn py_subscribe_transactions<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyAny>> {
        let client = self.client.clone();
        pyo3_async_runtimes::tokio::future_into_py(py, async move {
            client.subscribe_transactions().await.map_err(to_pyerr)
        })
    }

    /// Unsubscribe from transaction stream
    #[pyo3(name = "unsubscribe_transactions")]
    fn py_unsubscribe_transactions<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyAny>> {
        let client = self.client.clone();
        pyo3_async_runtimes::tokio::future_into_py(py, async move {
            client.unsubscribe_transactions().await.map_err(to_pyerr)
        })
    }

    /// Check if connected
    #[pyo3(name = "is_connected")]
    fn py_is_connected<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyAny>> {
        let client = self.client.clone();
        pyo3_async_runtimes::tokio::future_into_py(py, async move {
            Ok(client.is_connected().await)
        })
    }

    /// Disconnect from WebSocket
    #[pyo3(name = "disconnect")]
    fn py_disconnect<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyAny>> {
        let client = self.client.clone();
        pyo3_async_runtimes::tokio::future_into_py(py, async move {
            client.disconnect().await.map_err(to_pyerr)
        })
    }
}
