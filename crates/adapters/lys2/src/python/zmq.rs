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

//! Python bindings for Lys ZMQ client.

use pyo3::prelude::*;
use crate::zmq::LysZmqClient;
use crate::common::types::{LysTransactionRequest, LysTransactionResponse};

fn to_pyerr(err: impl std::fmt::Display) -> PyErr {
    pyo3::exceptions::PyRuntimeError::new_err(err.to_string())
}

/// Python wrapper for Lys ZMQ client
#[pyclass(name = "LysZmqClient")]
pub struct PyLysZmqClient {
    client: LysZmqClient,
}

#[pymethods]
impl PyLysZmqClient {
    /// Create a new Lys ZMQ client
    ///
    /// Parameters
    /// ----------
    /// endpoint : str
    ///     ZMQ endpoint (e.g., "ipc:///tmp/tx-executor.ipc")
    /// timeout_secs : int, optional
    ///     Operation timeout in seconds (default: 30)
    #[new]
    #[pyo3(signature = (endpoint, timeout_secs=None))]
    fn py_new(endpoint: String, timeout_secs: Option<u64>) -> PyResult<Self> {
        let client = LysZmqClient::new(endpoint, timeout_secs);
        Ok(Self { client })
    }

    /// Execute a transaction
    ///
    /// Parameters
    /// ----------
    /// request_json : str
    ///     JSON string of transaction request
    ///
    /// Returns
    /// -------
    /// str
    ///     JSON string of transaction response
    #[pyo3(name = "execute_transaction")]
    fn py_execute_transaction<'py>(
        &self,
        py: Python<'py>,
        request_json: String,
    ) -> PyResult<Bound<'py, PyAny>> {
        let client = self.client.clone();
        pyo3_async_runtimes::tokio::future_into_py(py, async move {
            // Parse request
            let request: LysTransactionRequest = serde_json::from_str(&request_json)
                .map_err(to_pyerr)?;

            // Execute
            let response = client.execute_transaction(&request).await.map_err(to_pyerr)?;

            // Serialize response
            let response_json = serde_json::to_string(&response).map_err(to_pyerr)?;
            Ok(response_json)
        })
    }

    /// Get the configured endpoint
    #[pyo3(name = "endpoint")]
    fn py_endpoint(&self) -> String {
        self.client.endpoint().to_string()
    }
}
