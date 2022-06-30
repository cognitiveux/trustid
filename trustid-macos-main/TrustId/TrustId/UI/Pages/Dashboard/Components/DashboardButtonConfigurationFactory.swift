//
//  DashboardConfigurationFactory.swift
//  TrustId
//
//  Created by Adamos Adamou on 30/11/21.
//

import Foundation
import SwiftUI

struct DashboardButtonConfigurationFactory{
    public func makeJoin() -> DashboardButtonConfiguration{
        return .init(
            identifier: "join",
            title: "Join Exam",
            iconName: "plus.app.fill",
            backgroundColor: TrustIdPalette.red
        )
    }
    
    public func makeView() -> DashboardButtonConfiguration{
        return .init(
            identifier: "view",
            title: "View Exams",
            iconName: "doc.plaintext.fill",
            backgroundColor: TrustIdPalette.profileBlue
        )
    }
}
