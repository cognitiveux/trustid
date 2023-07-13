//
//  DashboardSplitLayout.swift
//  TrustId
//
//  Created by Adamos Adamou on 5/12/21.
//

import SwiftUI

struct DashboardSplitLayout<LeftContent:View, RightContent:View>: View{
    
    public let leftContent: () -> LeftContent
    public let rightContent: () -> RightContent
    
    var body: some View{
        GeometryReader{ proxy in
            HStack(spacing:32){
                ZStack{
                    leftContent()
                        .frame(maxWidth:.infinity, maxHeight: .infinity, alignment: .trailing)
                }
                .frame(width: proxy.size.width*0.4 - 16)
                ZStack {
                    rightContent()
                        .frame(maxWidth:.infinity, maxHeight: .infinity, alignment: .leading)
                }
                .frame(width: proxy.size.width*0.6 - 16)
            }
        }
    }
}

struct DashboardSplitLayout_Previews: PreviewProvider {
    static var previews: some View {
        DashboardSplitLayout(leftContent: {
            Color.red
        }, rightContent: {
            Color.blue
        })
    }
}
