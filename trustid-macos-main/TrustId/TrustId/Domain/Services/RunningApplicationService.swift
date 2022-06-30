//
//  RunningApplicationService.swift
//  TrustId
//
//  Created by Adamos Adamou on 14/12/21.
//

import Foundation
import AppKit

struct RunningApplicationService{
    public func execute() -> [RunningApplication]{
        NSWorkspace
            .shared
            .runningApplications
            .map{
                .init(
                    name: $0.localizedName,
                    bundleIdentifier: $0.bundleIdentifier,
                    bundleURL: $0.bundleURL,
                    launchDate: $0.launchDate
                )
            }
    }
}
