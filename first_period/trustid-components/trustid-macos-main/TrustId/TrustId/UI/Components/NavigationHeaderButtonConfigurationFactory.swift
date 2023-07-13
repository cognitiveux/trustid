//
//  NavigationHeaderButtonConfigurationFactory.swift
//  TrustId
//
//  Created by Adamos Adamou on 3/1/22.
//

import Foundation

struct NavigationHeaderButtonConfigurationFactory{
    
    public struct Configuration{
        public let identifier:String
        public let title:String
        public let iconName:String
    }
    
    public func makeDashboard() -> Configuration{
        return .init(
            identifier: "dashboard",
            title: "Dashboard",
            iconName: "triangle"
        )
    }
    
    public func makeExaminations() -> Configuration{
        return .init(
            identifier: "examinations",
            title: "Examinations",
            iconName: "doc.plaintext"
        )
    }
    
    public func makeSettings() -> Configuration{
        return .init(
            identifier: "settings",
            title: "Settings",
            iconName: "gearshape"
        )
    }
}
