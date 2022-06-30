//
//  WebViewLegacy.swift
//  TrustId
//
//  Created by Adamos Adamou on 14/1/22.
//

import Foundation
import SwiftUI
import WebKit

extension WebViewLegacy{
    class Coordinator: NSObject, WKNavigationDelegate {
        private var viewModel: WebViewBaseViewModel
        
        init(_ viewModel: WebViewBaseViewModel) {
            self.viewModel = viewModel
        }

        func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
            self.viewModel.isLoading = false
        }
    }
}

struct WebViewLegacy: NSViewRepresentable {
 
    @ObservedObject var viewModel: WebViewBaseViewModel
    
    private let webView = WKWebView()

    func makeCoordinator() -> Coordinator {
        Coordinator(self.viewModel)
    }
    
    func makeNSView(context: Context) -> WKWebView {
        self.webView.navigationDelegate = context.coordinator

        if let url = URL(string: self.viewModel.url) {
            self.webView.load(URLRequest(url: url))
        }

        return self.webView
    }
    
    func updateNSView(_ uiView: WKWebView, context: Context) { }
}
