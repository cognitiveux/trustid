//
//  MockExamService.swift
//  TrustId
//
//  Created by Adamos Adamou on 11/1/22.
//

import Foundation

struct MockExamService{
    public static let exams:[Exam] = [
        .init(
            id: "834342543",
            name: "Human-Computer Interaction",
            status: "Started",
            scheduled: Date()
        ),
        .init(
            id: "895002221",
            name: "Introduction to Programming",
            status: "Upcoming",
            scheduled: Date()
        )
    ]
    
    public static let studentExams:[StudentExam] = [
        .init(
            id: "834342543",
            name: "Human-Computer Interaction",
            status: "Started",
            scheduled: Date(),
            privacyPolicy: "This is the privacy policy for TrustId app",
            additionalMaterial: true,
            duration: 120,
            examType: "Oral"
        ),
        .init(
            id: "895002221",
            name: "Introduction to Programming",
            status: "Upcoming",
            scheduled: Date(),
            privacyPolicy: "This is the privacy policy for TrustId app",
            additionalMaterial: true,
            duration: 120,
            examType: "Oral"
        )
    ]
    
    public static let instructorExams:[InstructorExam] = [
        .init(
            id: "834342543",
            name: "IN: Human-Computer Interaction",
            status: "Started",
            scheduled: Date(),
            privacyPolicy: "This is the privacy policy for TrustId app",
            additionalMaterial: true,
            duration: 120,
            examType: "Oral",
            enrolledStudents: [
                .init(email: "adam@trustid.com.eu", name: "Adamos Adamou", verificationStatus: "Pending"),
                .init(email: "marios@trustid.com.eu", name: "Marios Belk", verificationStatus: "Requested approval"),
                .init(email: "argyris@trustid.com.eu", name: "Argyris Constantinides", verificationStatus: "Verified")
            ]
        ),
        .init(
            id: "895002221",
            name: "IN: Introduction to Programming",
            status: "Upcoming",
            scheduled: Date(),
            privacyPolicy: "This is the privacy policy for TrustId app",
            additionalMaterial: true,
            duration: 120,
            examType: "Oral",
            enrolledStudents: [
                .init(email: "adam@trustid.com.eu", name: "Adamos Adamou", verificationStatus: "Pending"),
                .init(email: "marios@trustid.com.eu", name: "Marios Belk", verificationStatus: "Requested approval"),
                .init(email: "argyris@trustid.com.eu", name: "Argyris Constantinides", verificationStatus: "Verified")
            ]
        )
    ]
}
