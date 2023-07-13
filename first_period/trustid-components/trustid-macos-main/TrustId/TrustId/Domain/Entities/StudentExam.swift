//
//  StudentExam.swift
//  TrustId
//
//  Created by Adamos Adamou on 11/1/22.
//

import Foundation

struct StudentExam{
    let id:String
    let name:String
    let status:String
    let scheduled:Date
    let privacyPolicy:String
    let additionalMaterial:Bool
    let duration:Int
    let examType:String
    
    public var isStarted:Bool{
        return status.lowercased() == "started"
    }
    
    static var empty:StudentExam{
        .init(
            id: "-", name: "-", status: "-", scheduled: Date(), privacyPolicy: "-",
            additionalMaterial: true, duration: 0, examType: "-"
        )
    }
}
