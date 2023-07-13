//
//  ApiRequest.swift
//  TrustId
//
//  Created by Adamos Adamou on 8/12/21.
//

import Foundation

protocol ApiRequest: EndpointRoute, RequestHeaders, RequestBody, RequestExecutable { }

extension ApiRequest {
    
    public func execute<R:Decodable>(completion: @escaping (Result<R, HttpClientError>)->Void){
        let httpClient = URLSessionHttpClient()
        httpClient.execute(request: asURLRequest(), completion: completion)
    }
    
    private func asURLRequest() -> URLRequest {
        var request = URLRequest(url: path)
        request.httpMethod = method.rawValue.uppercased()
        headers.forEach{
            request.setValue($0.value, forHTTPHeaderField: $0.name)
        }
        if let body = body {
            request.httpBody = try! JSONEncoder().encode(body)
            request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        }
        return request
    }
}
