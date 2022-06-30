//
//  MockLiveExamService.swift
//  TrustId
//
//  Created by Adamos Adamou on 23/1/22.
//

import Foundation

struct MockLiveExamService{
    public static let enrolledStudents:[InstructorLiveExaminationView.EnrolledStudent] = [
        .init(email: "argyris@trustid.com", name: "Argyris", surname: "Constantinides", status: "Verified"),
        .init(email: "marios@trustid.com", name: "Marios", surname: "Belk", status: "Requested approval"),
        .init(email: "adam@trustid.com", name: "Adam", surname: "Adamou", status: "Pending")
    ]
}
