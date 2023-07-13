//
//  WebViewBaseViewModel.swift
//  TrustId
//
//  Created by Adamos Adamou on 14/1/22.
//

import Foundation

final class WebViewBaseViewModel: ObservableObject {
    @Published var url: String
    @Published var isLoading: Bool = true
    
    init (url: String) {
        self.url = url
    }
}
