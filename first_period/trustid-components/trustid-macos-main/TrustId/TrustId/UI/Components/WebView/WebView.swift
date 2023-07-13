//
//  WebView.swift
//  TrustId
//
//  Created by Adamos Adamou on 16/12/21.
//

import SwiftUI
import WebKit

struct WebView:View{
    
    public let url: String

    var body: some View{
        WebViewBaseView(viewModel: .init(url: url))
    }
}

struct WebView_Previews: PreviewProvider {
    static var previews: some View {
        WebView(url: "https://www.apple.com")
    }
}
