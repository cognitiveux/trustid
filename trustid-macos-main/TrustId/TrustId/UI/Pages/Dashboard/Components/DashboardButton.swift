//
//  DashboardButton.swift
//  TrustId
//
//  Created by Adamos Adamou on 30/11/21.
//

import SwiftUI

struct DashboardButton: View {

    public let configuration: DashboardButtonConfiguration
    
    var body: some View{
        VStack(spacing:8){
            ZStack{
                configuration.backgroundColor
                    .cornerRadius(24)
                
                Image(systemName: configuration.iconName)
                    .resizable()
                    .frame(width: 30, height: 30)
                    .foregroundColor(.white)
                    .cornerRadius(8)
                    
            }
            .frame(width: 80, height: 80)
            
            Text(configuration.title)
                .font(.custom("Roboto", size: 13))
        }
    }
}

struct DashboardButton_Previews: PreviewProvider {
    
    static var configuration:DashboardButtonConfiguration = .init(
        identifier: "join",
        title: "Join Exam",
        iconName: "cross",
        backgroundColor: .red
    )
    
    static var previews: some View {
        DashboardButton(configuration: configuration)
    }
}
