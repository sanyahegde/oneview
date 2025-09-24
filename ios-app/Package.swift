// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "PortfolioAI",
    platforms: [
        .iOS(.v16)
    ],
    products: [
        .library(
            name: "PortfolioAI",
            targets: ["PortfolioAI"]
        ),
    ],
    dependencies: [
        // Add any external dependencies here
    ],
    targets: [
        .target(
            name: "PortfolioAI",
            dependencies: [],
            path: "PortfolioAI"
        ),
        .testTarget(
            name: "PortfolioAITests",
            dependencies: ["PortfolioAI"],
            path: "PortfolioAITests"
        ),
    ]
)
