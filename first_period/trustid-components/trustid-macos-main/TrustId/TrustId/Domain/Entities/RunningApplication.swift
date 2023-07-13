//
//  RunningApplication.swift
//  TrustId
//
//  Created by Adamos Adamou on 14/12/21.
//

import Foundation

struct RunningApplication:Identifiable{
    let id = UUID()
    let name:String?
    let bundleIdentifier:String?
    let bundleURL:URL?
    let launchDate:Date?
}
