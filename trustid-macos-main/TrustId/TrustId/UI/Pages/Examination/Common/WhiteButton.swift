//
//  WhiteButton.swift
//  TrustId
//
//  Created by Adamos Adamou on 30/11/21.
//

import SwiftUI

struct WhiteButton: ButtonStyle {
    
    public var isSelected = false
    
    func makeBody(configuration: Configuration) -> some View {
        return isSelected
            ? AnyView(makeBodySelected(configuration: configuration))
            : AnyView(makeBodyNotSelected(configuration: configuration))
    }
    
    private func makeBodySelected(configuration: Configuration) -> some View{
        configuration.label
            .lineLimit(1)
            .padding(8)
            .background(TrustIdPalette.lightGray)
            .foregroundColor(.black)
            .clipShape(
                RoundedRectangle(cornerRadius: 8)
            )
    }
    
    private func  makeBodyNotSelected(configuration: Configuration) -> some View{
        configuration.label
            .lineLimit(1)
            .padding(8)
            .background(Color.white)
            .foregroundColor(.black)
            .overlay(
                RoundedRectangle(cornerRadius: 8)
                    .stroke(TrustIdPalette.lightGray, style: StrokeStyle(lineWidth: 1))
            )
    }
}
