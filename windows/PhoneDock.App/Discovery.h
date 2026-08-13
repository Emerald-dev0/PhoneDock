#pragma once

#include <windows.h>
#include <windns.h>
#include <string>
#include <vector>
#include <functional>
#include <mutex>

namespace PhoneDock::App {

struct DiscoveredService {
    std::wstring instanceName;
    std::wstring hostName;
    std::wstring ipAddress;
    uint16_t port;
};

class DiscoveryAgent {
public:
    DiscoveryAgent();
    ~DiscoveryAgent();

    void StartBrowsing(std::function<void(const DiscoveredService&)> onServiceFound);
    void StopBrowsing();

private:
    static VOID WINAPI BrowseCallback(DWORD status, PVOID context, PDNS_RECORD record);
    static VOID WINAPI ResolveCallback(DWORD status, PVOID context, PDNS_SERVICE_INSTANCE instance);

    DNS_SERVICE_CANCEL m_cancelHandle;
    std::function<void(const DiscoveredService&)> m_onServiceFound;
    bool m_isBrowsing;
    std::mutex m_mutex;
};

} // namespace PhoneDock::App
