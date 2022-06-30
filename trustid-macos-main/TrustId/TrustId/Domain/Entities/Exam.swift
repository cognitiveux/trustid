//
//  Exam.swift
//  TrustId
//
//  Created by Adamos Adamou on 25/11/21.
//

import Foundation

struct Exam{
    let id:String
    let name:String
    let status:String
    let scheduled:Date
    
    public var isStarted:Bool{
        return status.lowercased() == "started"
    }
    
    static var empty:Exam{
        .init(id: "-", name: "-", status: "-", scheduled: Date())
    }
}
