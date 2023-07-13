//
//  NavigationHeaderViewModifier.swift
//  TrustId
//
//  Created by Adamos Adamou on 3/1/22.
//

import SwiftUI

struct NavigationHeaderViewModifier: ViewModifier{
    public let showOnlyLogo:Bool
    
    func body(content: Content) -> some View {
        VStack(spacing:0){
            NavigationHeaderView(showOnlyLogo: showOnlyLogo)
                .frame(height:55)
                .clipped()
            
            content
        }
    }
}

extension View{
    func addNavigationHeader(showOnlyLogo:Bool = false) -> some View{
        modifier(NavigationHeaderViewModifier(showOnlyLogo: showOnlyLogo))
    }
}
