#include <iostream>
#include <chrono>
#include <thread>
#include <filesystem>
#include <string>
#include <vector>
#include <cstdlib>
#include <csignal>
#include <atomic>
#include <sstream>

namespace fs = std::filesystem;
std::atomic<bool> ctrlc_pressed(false);
bool deleted = false;

namespace ewfts {
	void sleep(int n) {
		std::this_thread::sleep_for(std::chrono::milliseconds(n));
	}
	bool isfile(const fs::path& dir) {
		return fs::is_regular_file(dir);
	}
	bool isfolder(const fs::path& dir) {
		return fs::is_directory(dir);
	}
	void rm(const fs::path& dir) {
		if (!fs::exists(dir)) {
			std::cout << "Path Doesn't Exist" << std::endl;
			return;
		}
		fs::remove_all(dir);
	}
	std::vector<std::string> parse(int arg, char* args[]) {
		std::string one;
		for (int i = 1; i < arg; i++) {
			one += args[i];
			one += " ";
		}
		std::stringstream ss(one);
		std::vector<std::string> joined;
		std::string tmp;
		while (ss >> tmp) {
			if (isfile(tmp) || isfolder(tmp)) {
				joined.push_back(tmp);
			}
		}
		return joined;
	}
	void list(const std::vector<std::string>& list) {
		for (int i = 0; i < list.size(); i++) {
			if (isfile(list[i])) {
				std::cout << i+1 << ". " << list[i] << " (File)" << std::endl;
			}
			else if (isfolder(list[i])) {
				std::cout << i+1 << ". " << list[i] << " (Folder)" << std::endl;
			}
			else {
				std::cout << i+1 << ". " << list[i] << " (Other)" << std::endl;
			}
		}
	}
	std::string cmd(int arg, char* args[]) {
		std::string joined;
		for (int i = 1; i < arg; i++) {
			joined = joined + args[i];
			joined = joined + " ";
		}
		if (!joined.empty()) {
			joined.pop_back();
		}
		return joined;
	}
	void handle(int) {
		ctrlc_pressed.store(true, std::memory_order_relaxed);
	}
}

int main(int argc, char* argv[]) {
	std::signal(SIGINT, ewfts::handle);
	std::vector<std::string> test = ewfts::parse(argc, argv);
	if (argc == 1) {
		std::cout << "EWFTS v2.0 (C++)" << std::endl;
		std::cout <<    "█████████████████████████████████████\n"
				"█████████████████████████████████████\n"
				"████ ▄▄▄▄▄ ██▄▄ ▀ ▀▄█  █▀█ ▄▄▄▄▄ ████\n"
				"████ █   █ █▀▄  █▀▄█▄▀▄ ▀█ █   █ ████\n"
				"████ █▄▄▄█ █▄▀ █▄▀ ▀▄█ ▄ █ █▄▄▄█ ████\n"
				"████▄▄▄▄▄▄▄█▄▀▄█ █▄▀▄█▄▀ █▄▄▄▄▄▄▄████\n"
				"████▄▄▀█▀ ▄▄▀▄ █▄▄ ▄▀ ▀ ▀██▀ ▄▀▀█████\n"
				"████▀█ ▀ █▄▀ ▄▀ ▄▄ ▀ ▄▀▀ ▄▀  ▀███████\n"
				"████ ▄ █▀▀▄ ▄▄ █▀▄█▄█▄▀  █  ▀██▀ ████\n"
				"████ ▄█▀█▄▄▀ ▀ █▀▄▄ █▀ ▀▀▀▀▀ ▄ █▀████\n"
				"████ █▄  ▄▄██▀▀█▄▄▀▄ ▄▀▀ ▀▀▀▀▄ ▀▀████\n"
				"████ ▄▄▄▀▀▄▄▀▀█▀▄▄▄▀ █▄ ▀▄ ▀█▄██▄████\n"
				"████▄█▄▄█▄▄█▀██▄▀▀▀▄▄▄▄▄ ▄▄▄ ▀▄▄▄████\n"
				"████ ▄▄▄▄▄ █   █▀ ▄▀█▄▄  █▄█ ▄▄▀█████\n"
				"████ █   █ ██ █▄▄▄█▄▄▄▄▄  ▄▄▄ ▀ █████\n"
				"████ █▄▄▄█ █▀ ▄ ▄██▀ ▄▄▄▄   ▄  ▄▀████\n"
				"████▄▄▄▄▄▄▄█▄██▄███▄██▄███▄█▄█▄██████\n"
				"█████████████████████████████████████\n"
				"█████████████████████████████████████" << std::endl;
		return 0;
	}
	if (test.size() == 0) {
		std::string command = ewfts::cmd(argc, argv);
		std::system(command.c_str());
		return 0;
	}
	ewfts::list(test);
	std::string answer;
	std::cout << "Select Target to delete (or type 'exit' to cancel): ";
	std::getline(std::cin, answer);
	if (answer == "exit") {
		return 0;
	} else if (answer == "none") {
		std::string command = ewfts::cmd(argc, argv);
		std::system(command.c_str());
		return 0;
	}
	int choice;
	try {
		choice = std::stoi(answer);
	} catch (...) {
		std::cout << "not int!" << std::endl;
		return 1;
	}
	if (choice < 1 || choice > test.size()) {
		std::cout << "Out of range.\n";
		return 1;
	}
	answer = test[choice - 1];
	std::string command = ewfts::cmd(argc, argv);
	std::system(command.c_str());
	std::cout << "Finished. Cleaning up in 5 seconds... (CTRL+C to cancel)" << std::endl;
	for (int i = 0; i < 5 && !ctrlc_pressed; ++i) ewfts::sleep(1000);
	if (ctrlc_pressed) {
		std::cout << "Cleanup cancelled. Target retained.\n";
		return 0;
	}

	for (int i = 0; i < 5; ++i) {
		try {
			ewfts::rm(answer);
			std::cout << "Deleted successfully.\n";
			deleted = true;
			break;
		}
		catch (const std::filesystem::filesystem_error&) {
			ewfts::sleep(500);
		}
	}

	if (!deleted) {
		std::cerr << "Failed to delete: File is still locked.\n";
		return 1;
	}
	return 0;
}
