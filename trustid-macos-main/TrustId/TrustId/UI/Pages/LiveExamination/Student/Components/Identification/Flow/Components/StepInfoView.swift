//
//  StepInfoView.swift
//  TrustId
//
//  Created by Adamos Adamou on 29/12/21.
//

import SwiftUI

struct StepInfoView<Action:View>:View{
    
    public let title:String
    public let subTitle:String?
    public let actionContainer:() -> Action
    
    var body: some View{
        VStack(alignment:.center){
            Text(title)
                .frame(maxHeight: .infinity)
                .font(.custom("Roboto", size: 20))
            if let subTitle = subTitle{
                Text(subTitle)
                    .frame(maxHeight: .infinity)
                    .font(.custom("Roboto", size: 15))
            }
            actionContainer()
                .frame(maxHeight: .infinity)
        }
    }
}

struct StepInfoView_Previews: PreviewProvider {
    static var previews: some View {
        StepInfoView(title: "Title", subTitle: "Subtitle"){
            Button("Button"){ }
        }
    }
}
