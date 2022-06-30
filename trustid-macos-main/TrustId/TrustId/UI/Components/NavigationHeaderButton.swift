//
//  NavigationHeaderButton.swift
//  TrustId
//
//  Created by Adamos Adamou on 3/1/22.
//

import SwiftUI

struct NavigationHeaderButton: View {
        
    public typealias Configuration = NavigationHeaderButtonConfigurationFactory.Configuration
    
    public let configuration: Configuration
    
    var body: some View {
        VStack(spacing:4){
            Image(systemName: configuration.iconName)
                .resizable()
                .frame(width: 20, height: 20)
            
            Text(configuration.title)
                .font(.custom("Roboto", size: 13))
        }
    }
}

struct NavigationHeaderButton_Previews: PreviewProvider {
    
    static var configuration:NavigationHeaderButton.Configuration = .init(
        identifier: "dashboard",
        title: "Dashboard",
        iconName: "triangle"
    )
    
    static var previews: some View {
        NavigationHeaderButton(configuration: configuration)
    }
}
