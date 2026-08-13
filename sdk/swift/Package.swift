// swift-tools-version:5.9
import PackageDescription
let package=Package(name:"CosmosSynapse",products:[.library(name:"CosmosSynapse",targets:["CosmosSynapse"])],targets:[.target(name:"CosmosSynapse"),.testTarget(name:"CosmosSynapseTests",dependencies:["CosmosSynapse"])])
