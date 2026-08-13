#include "SessionClient.h"
#include <iostream>

#pragma comment(lib, "ws2_32.lib")

namespace PhoneDock::App {

SessionClient::SessionClient() : m_socket(INVALID_SOCKET), m_isConnected(false) {
    WSADATA wsaData;
    WSAStartup(MAKEWORD(2, 2), &wsaData);
}

SessionClient::~SessionClient() {
    Disconnect();
    WSACleanup();
}

bool SessionClient::Connect(const std::wstring& ipAddress, uint16_t port) {
    m_socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (m_socket == INVALID_SOCKET) return false;

    sockaddr_in serverAddr;
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(port);

    char ip[INET_ADDRSTRLEN];
    WideCharToMultiByte(CP_UTF8, 0, ipAddress.c_str(), -1, ip, INET_ADDRSTRLEN, NULL, NULL);
    inet_pton(AF_INET, ip, &serverAddr.sin_addr);

    if (connect(m_socket, (sockaddr*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR) {
        closesocket(m_socket);
        return false;
    }

    m_isConnected = true;
    return true;
}

void SessionClient::Disconnect() {
    m_isConnected = false;
    if (m_socket != INVALID_SOCKET) {
        closesocket(m_socket);
        m_socket = INVALID_SOCKET;
    }
    if (m_receiveThread.joinable()) {
        m_receiveThread.join();
    }
}

void SessionClient::StartListening(std::function<void(const std::vector<uint8_t>&, bool)> onFrameReceived) {
    m_receiveThread = std::thread([this, onFrameReceived]() {
        while (m_isConnected) {
            uint32_t frameSize = 0;
            int bytesRead = recv(m_socket, (char*)&frameSize, 4, 0);
            if (bytesRead <= 0) break;

            frameSize = ntohl(frameSize); // Android sends in Big Endian

            uint8_t flags = 0;
            bytesRead = recv(m_socket, (char*)&flags, 1, 0);
            if (bytesRead <= 0) break;

            bool isKeyFrame = (flags == 1);

            std::vector<uint8_t> buffer(frameSize);
            size_t totalReceived = 0;
            while (totalReceived < frameSize) {
                bytesRead = recv(m_socket, (char*)buffer.data() + totalReceived, (int)(frameSize - totalReceived), 0);
                if (bytesRead <= 0) break;
                totalReceived += bytesRead;
            }

            if (totalReceived == frameSize) {
                onFrameReceived(buffer, isKeyFrame);
            }
        }
        m_isConnected = false;
    });
}

} // namespace PhoneDock::App
