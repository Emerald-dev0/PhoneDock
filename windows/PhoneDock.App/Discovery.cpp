#include "Discovery.h"
#include <iostream>

#pragma comment(lib, "dnsapi.lib")

namespace PhoneDock::App {

DiscoveryAgent::DiscoveryAgent() : m_cancelHandle({0}), m_isBrowsing(false) {}

DiscoveryAgent::~DiscoveryAgent() {
    StopBrowsing();
}

void DiscoveryAgent::StartBrowsing(std::function<void(const DiscoveredService&)> onServiceFound) {
    std::lock_guard<std::mutex> lock(m_mutex);
    if (m_isBrowsing) return;

    m_onServiceFound = onServiceFound;

    DNS_SERVICE_BROWSE_REQUEST browseRequest = { 0 };
    browseRequest.Version = DNS_QUERY_REQUEST_VERSION1;
    browseRequest.InterfaceIndex = 0;
    browseRequest.QueryName = L"_phonedock._tcp.local";
    browseRequest.pBrowseCallback = BrowseCallback;
    browseRequest.pQueryContext = this;

    DNS_STATUS status = DnsServiceBrowse(&browseRequest, &m_cancelHandle);
    if (status == DNS_REQUEST_PENDING) {
        m_isBrowsing = true;
    }
}

void DiscoveryAgent::StopBrowsing() {
    std::lock_guard<std::mutex> lock(m_mutex);
    if (!m_isBrowsing) return;

    DnsServiceBrowseCancel(&m_cancelHandle);
    m_isBrowsing = false;
}

VOID WINAPI DiscoveryAgent::BrowseCallback(DWORD status, PVOID context, PDNS_RECORD record) {
    auto agent = static_cast<DiscoveryAgent*>(context);

    if (status == ERROR_SUCCESS && record != nullptr) {
        if (record->wType == DNS_TYPE_PTR) {
            DNS_SERVICE_RESOLVE_REQUEST resolveRequest = { 0 };
            resolveRequest.Version = DNS_QUERY_REQUEST_VERSION1;
            resolveRequest.InterfaceIndex = record->dwInterfaceIndex;
            resolveRequest.QueryName = record->Data.PTR.pNameHost;
            resolveRequest.pResolveCallback = ResolveCallback;
            resolveRequest.pQueryContext = agent;

            // Resolve the service to get IP and Port
            DnsServiceResolve(&resolveRequest, nullptr); // Not storing cancel handle for resolve
        }
        DnsRecordListFree(record, DnsFreeRecordList);
    }
}

VOID WINAPI DiscoveryAgent::ResolveCallback(DWORD status, PVOID context, PDNS_SERVICE_INSTANCE instance) {
    auto agent = static_cast<DiscoveryAgent*>(context);

    if (status == ERROR_SUCCESS && instance != nullptr) {
        DiscoveredService service;
        service.instanceName = instance->pszInstanceName;
        service.hostName = instance->pszHostName;
        service.port = instance->wPort;

        if (instance->ip4Address != nullptr) {
            service.ipAddress = instance->ip4Address; // Simplification for example
        }

        if (agent->m_onServiceFound) {
            agent->m_onServiceFound(service);
        }

        DnsServiceFreeInstance(instance);
    }
}

} // namespace PhoneDock::App
