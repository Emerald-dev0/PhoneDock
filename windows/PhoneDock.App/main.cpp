#include <iostream>
#include <thread>
#include "Discovery.h"

int main() {
    std::wcout << L"PhoneDock Windows Discovery Agent starting..." << std::endl;

    PhoneDock::App::DiscoveryAgent agent;

    agent.StartBrowsing([](const PhoneDock::App::DiscoveredService& service) {
        std::wcout << L"-------------------------------------------" << std::endl;
        std::wcout << L"Found PhoneDock Device!" << std::endl;
        std::wcout << L"Instance: " << service.instanceName << std::endl;
        std::wcout << L"Host:     " << service.hostName << std::endl;
        std::wcout << L"IP:       " << service.ipAddress << std::endl;
        std::wcout << L"Port:     " << service.port << std::endl;
        std::wcout << L"-------------------------------------------" << std::endl;
    });

    std::cout << "Press Enter to exit..." << std::endl;
    std::cin.get();

    agent.StopBrowsing();
    std::cout << "Exiting..." << std::endl;

    return 0;
}
