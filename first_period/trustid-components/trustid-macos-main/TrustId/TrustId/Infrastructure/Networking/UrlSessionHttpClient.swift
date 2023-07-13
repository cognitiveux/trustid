//
//  URLSessionHttpClient.swift
//  
//
//  Created by Adamos Adamou on 20/1/21.
//

import Foundation

final class URLSessionHttpClient:HttpClient{
    
    func execute<T>(request: URLRequest, completion: @escaping (Result<T, HttpClientError>) -> Void) where T : Decodable {
        URLSession.shared.dataTask(with: request) { data, response, error in
            DispatchQueue.main.async {
                do{
                    if let error = error{
                        completion(.failure(.failed(error)))
                        return
                    }
                    
                    guard
                        let httpResponse = response as? HTTPURLResponse,
                        let data = data
                    else {
                        return completion(.failure(.noData))
                    }
                    
                    guard (200...201).contains(httpResponse.statusCode) else {
                        
                        if httpResponse.statusCode == 401{
                            
                            AuthenticationTokenService.shared.access = nil
                            AuthenticationTokenService.shared.refresh = nil
                            
                            NotificationCenter.default
                                .post(name: .userAuthenticatedNotification, object: nil)
                            
                            return completion(.failure(.apiErrorResponse(httpResponse.statusCode, .init(message: "Unauthorized"))))
                        }
                        
                        if let decodedErrorObject = try? JSONDecoder().decode(HttpClientErrorModel.self, from: data){
                            return completion(.failure(.apiErrorResponse(httpResponse.statusCode, decodedErrorObject)))
                        }
                        return completion(.failure(.apiErrorResponse(httpResponse.statusCode, .init(message: "Can't decode error response model"))))
                    }
                    
                    let decodedObject = try JSONDecoder().decode(T.self, from: data)
                    
                    completion(.success(decodedObject))
                } catch{
                    completion(.failure(.failed(error)))
                }
            }
        }.resume()
    }
}
