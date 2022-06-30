//
//  RedButton.swift
//  TrustId
//
//  Created by Adamos Adamou on 30/11/21.
//

import SwiftUI

struct RedButton: ButtonStyle {
    
    public var width:CGFloat? = nil
    public var height:CGFloat? = nil
    
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .lineLimit(1)
            .padding(8)
            .frame(width: width, height: height)
            .background(TrustIdPalette.red)
            .foregroundColor(.white)
            .clipShape(RoundedRectangle(cornerRadius: 8))
    }
}
