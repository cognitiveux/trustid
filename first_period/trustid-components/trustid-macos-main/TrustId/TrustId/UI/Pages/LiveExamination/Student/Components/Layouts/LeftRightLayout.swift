//
//  LeftRightLayout.swift
//  TrustId
//
//  Created by Adamos Adamou on 29/12/21.
//

import SwiftUI

struct LeftRightLayout<LeftContent:View, RightContent:View>: View {
    
    public let leftWidthPercentage:CGFloat
    public let leftContent: () -> LeftContent
    public let rightContent: () -> RightContent
    
    var body: some View {
        GeometryReader{ proxy in
            HStack(spacing:0){
                leftContent()
                    .frame(width:proxy.size.width * leftWidthPercentage)
                rightContent()
                    .frame(width:proxy.size.width * (1-leftWidthPercentage))
            }
        }
    }
}

struct LeftRightLayout_Previews: PreviewProvider {
    static var previews: some View {
        LeftRightLayout(leftWidthPercentage: 0.75){
            Color.red
        } rightContent: {
            Color.blue
        }
    }
}
