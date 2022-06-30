//
//  MaximumHeightPreferenceKey.swift
//  TrustId
//
//  Created by Adamos Adamou on 4/12/21.
//

import Foundation
import SwiftUI

struct MaximumHeightPreferenceKey: PreferenceKey {
    static let defaultValue: CGFloat = 0
    
    static func reduce(value: inout CGFloat, nextValue: () -> CGFloat) {
        value = max(value, nextValue())
    }
}
