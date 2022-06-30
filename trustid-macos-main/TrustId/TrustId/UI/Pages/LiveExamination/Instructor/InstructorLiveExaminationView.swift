//
//  InstructorLiveExaminationView.swift
//  TrustId
//
//  Created by Adamos Adamou on 16/12/21.
//

import SwiftUI

extension InstructorLiveExaminationView{
    struct EnrolledStudent:Identifiable{
        let id = UUID()
        let email:String
        let name:String
        let surname:String
        let status:String
        let hasRequestedApproval:Bool = false
        
        var fullname:String {
            return "\(name) \(surname)"
        }
        
        var initials:String{
            guard
                let nameFirstLetter = name.first,
                let surnameFirstLetter = surname.first
            else {
                return "-"
            }
            
            return "\(nameFirstLetter.uppercased())\(surnameFirstLetter.uppercased())"
        }
    }
    
    enum EnrolledStudentFilter:String, CaseIterable, Identifiable{
        case all = "All"
        case verified = "Verified"
        case pending = "Pending"
        case requestedApproval = "Requested approval"
        
        var id: String { self.rawValue }
    }
}

struct InstructorLiveExaminationView: View {
    
    @StateObject public var viewModel:InstructorLiveExaminationViewModel
    
    @State private var selectedFilter:EnrolledStudentFilter = .all
    
    private static let refreshSeconds:Double = 5
    
    private let timer = Timer
        .publish(every: refreshSeconds, on: .main, in: .common)
        .autoconnect()
    
    var body: some View {
        StudentLiveExaminationLayout {
            mainContentView
                .padding(.horizontal, 64)
                .padding(.vertical, 32)
        } statusContent: {
            statusContentView
        } actionContent: {
            actionContentView
        }
        .background(Color.white)
        .onAppear(perform: viewModel.loadEnrolledStudents)
        .addNavigationHeader(showOnlyLogo: true)
        //.overlay(LoadingView(isLoading: viewModel.isLoading))
        .onReceive(timer, perform: runRefresh)
    }
    
    private func runRefresh(date:Date){
        viewModel.loadEnrolledStudents()
    }
    
    private var mainContentView: some View{
        GeometryReader { reader in
            VStack(spacing:16){
                Text("Student's List")
                    .font(.custom("Roboto", size: 20))
                    .bold()
                
                Picker("Filter", selection: $selectedFilter){
                    ForEach(EnrolledStudentFilter.allCases) { filter in
                        Text(filter.rawValue).tag(filter)
                    }
                }
                .labelsHidden()
                .pickerStyle(.segmented)
                .frame(width: reader.size.width * 0.6)
                
                EnrolledStudentsListView(
                    enrolledStudents: viewModel.enrolledStudents, filter: selectedFilter.rawValue
                ) { approvedStudent in
                    viewModel.approvedStudent(student: approvedStudent)
                }
            }
        }
    }
    
    private var statusContentView: some View{
        VStack{
            Text("Alerts")
                .font(.custom("Roboto", size: 13))
                .bold()
            
            AlertListView(alerts: viewModel.alerts)
            
            Spacer()
        }
    }
    
    private var actionContentView: some View{
        HStack{
            Spacer()
            
            Button("Close Exam") {
                viewModel.closeExam()
            }
            .font(.custom("Roboto", size: 13))
            .buttonStyle(RedButton())
        }
        .padding()
    }
}

struct InstructorLiveExaminationView_Previews: PreviewProvider {
    static var previews: some View {
        InstructorLiveExaminationView(
            viewModel: .init(exam_id: "test_exam_id")
        )
    }
}
