//
//  BlueButton.swift
//  TrustId
//
//  Created by Adamos Adamou on 30/11/21.
//

import SwiftUI

struct BlueButton: ButtonStyle {
    
    @Environment(\.isEnabled) var isEnabled
    
    public var width:CGFloat? = nil
    public var height:CGFloat? = nil
    
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .lineLimit(1)
            .padding(8)
            .frame(width: width, height: height)
            .background(TrustIdPalette.buttonBlue)
            .foregroundColor(.white)
            .clipShape(RoundedRectangle(cornerRadius: 8))
            .opacity(isEnabled ? 1 : 0.6)
    }
}
