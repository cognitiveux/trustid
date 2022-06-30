//
//  WebViewBase.swift
//  TrustId
//
//  Created by Adamos Adamou on 14/1/22.
//

import SwiftUI

struct WebViewBaseView:View{
    @StateObject var viewModel: WebViewBaseViewModel
    
    var body: some View {
        WebViewLegacy(viewModel: viewModel)
            .overlay(LoadingView(isLoading: viewModel.isLoading))
    }
}

struct WebViewBase_Previews: PreviewProvider {
    static var previews: some View {
        WebViewBaseView(viewModel: .init(url: "https://www.apple.com/au/"))
    }
}
