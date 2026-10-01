#pragma once

#include <winsock2.h>
#include <ws2tcpip.h>
#include <windows.h>
#include <cstdint>
#include <functional>
#include <string>
#include <thread>
#include <vector>

namespace PhoneDock::App {

class SessionClient {
public:
    SessionClient();
    ~SessionClient();

    bool Connect(const std::wstring& ipAddress, uint16_t port);
    void Disconnect();
    void StartListening(std::function<void(const std::vector<uint8_t>&, bool)> onFrameReceived);

private:
    SOCKET m_socket;
    bool m_isConnected;
    std::thread m_receiveThread;
};

} // namespace PhoneDock::App
