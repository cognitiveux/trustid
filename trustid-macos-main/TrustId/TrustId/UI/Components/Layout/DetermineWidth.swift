//
//  DetermineWidth.swift
//  TrustId
//
//  Created by Adamos Adamou on 4/12/21.
//

import Foundation
import SwiftUI

struct DetermineWidth: View {
    typealias Key = MaximumWidthPreferenceKey
    
    var body: some View {
        GeometryReader { proxy in
            Color
                .clear
                .anchorPreference(key: Key.self, value: .bounds) { anchor in
                    proxy[anchor].size.width
                }
        }
    }
}
