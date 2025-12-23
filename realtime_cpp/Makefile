CXX = g++
CXXFLAGS = -std=c++11 -Wall -O2
LDFLAGS = -lportaudio

TARGET = guitar_processor
SRC_DIR = src
BUILD_DIR = build

SOURCES = $(SRC_DIR)/main.cpp $(SRC_DIR)/effects.cpp $(SRC_DIR)/processor.cpp
OBJECTS = $(SOURCES:$(SRC_DIR)/%.cpp=$(BUILD_DIR)/%.o)

all: $(BUILD_DIR) $(TARGET)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(TARGET): $(OBJECTS)
	$(CXX) $(OBJECTS) -o $(TARGET) $(LDFLAGS)
	@echo "build complete: ./$(TARGET)"

$(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -rf $(BUILD_DIR) $(TARGET)

install-deps:
	@echo "install portaudio development libraries:"
	@echo "  ubuntu/debian: sudo apt-get install portaudio19-dev"
	@echo "  arch: sudo pacman -S portaudio"
	@echo "  macos: brew install portaudio"

run: $(TARGET)
	./$(TARGET)

.PHONY: all clean install-deps run
