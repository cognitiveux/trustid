//
//  TrustIdApp.swift
//  TrustId
//
//  Created by Adamos Adamou on 22/11/21.
//

import SwiftUI

@main
struct TrustIdApp: App {
    var body: some Scene {
        WindowGroup {
            ApplicationContainerView()
                .frame(minWidth: 1300, idealWidth: .infinity, maxWidth: .infinity, minHeight: 700, idealHeight: .infinity, maxHeight: .infinity)
                .environmentObject(ApplicationContainerViewModel())
                .preferredColorScheme(.light)
                .navigationTitle("TRUSTID")
        }
    }
}
