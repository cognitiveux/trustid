//
//  SplitViewLayout.swift
//  TrustId
//
//  Created by Adamos Adamou on 29/12/21.
//

import SwiftUI

struct SplitViewLayout<T:View, B:View>:View{
    
    public let topContent:() -> T
    public let bottomContent:() -> B
    
    var body: some View{
        GeometryReader{ proxy in
            VStack(spacing:0){
                topContent()
                    .frame(height: proxy.size.height*0.75)
                bottomContent()
                    .frame(height: proxy.size.height*0.25)
            }
        }
    }
}

struct SplitViewLayout_Previews: PreviewProvider {
    static var previews: some View {
        SplitViewLayout{
            VStack{
                Text("TopContent")
                    .font(.custom("Roboto", size: 13))
            }.background(Color.blue)
        } bottomContent: {
            VStack{
                Text("BottomContent")
                    .font(.custom("Roboto", size: 13))
            }.background(Color.red)
        }
    }
}
