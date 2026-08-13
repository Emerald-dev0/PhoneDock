package com.phonedock.app.ui.dashboard

import androidx.lifecycle.ViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

data class DashboardUiState(
    val isServiceRunning: Boolean = false,
    val connectedDevice: String? = null,
    val localIp: String = "Unknown",
    val localPort: Int? = null,
    val connectionType: String = "None"
)

class DashboardViewModel : ViewModel() {
    private val _uiState = MutableStateFlow(DashboardUiState())
    val uiState: StateFlow<DashboardUiState> = _uiState.asStateFlow()

    fun toggleService() {
        // TODO: Implement binding to ConnectionService to control it
        _uiState.value = _uiState.value.copy(
            isServiceRunning = !_uiState.value.isServiceRunning
        )
    }
}
