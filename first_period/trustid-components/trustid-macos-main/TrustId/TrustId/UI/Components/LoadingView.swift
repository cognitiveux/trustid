//
//  LoadingView.swift
//  TrustId
//
//  Created by Adamos Adamou on 5/12/21.
//

import SwiftUI

struct LoadingView: View{
    
    public let isLoading:Bool
    
    var body: some View{
        if isLoading{
            return AnyView(loadingView)
        }
        return AnyView(EmptyView())
    }
    
    private var loadingView:some View{
        ZStack{
            Color.gray
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                .opacity(0.6)
                .blur(radius: 3)
            
            ProgressView()
                .progressViewStyle(CircularProgressViewStyle())
                .aspectRatio(contentMode: .fit)
        }
    }
}

struct LoadingView_Previews: PreviewProvider {
  
    static var isLoading = false
    
    static var previews: some View {
        LoadingView(isLoading: isLoading)
            .previewLayout(.sizeThatFits)
            .frame(width: 150, height: 300, alignment: /*@START_MENU_TOKEN@*/.center/*@END_MENU_TOKEN@*/)
    }
}
