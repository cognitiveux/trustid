//
//  ApplicationContainerView.swift
//  TrustId
//
//  Created by Adamos Adamou on 22/11/21.
//

import SwiftUI

struct ApplicationContainerView: View {
    
    @EnvironmentObject
    var viewModel:ApplicationContainerViewModel
    
    var body: some View {
        if viewModel.isLoggedIn{
            page
        } else {
            LoginPageView()
        }
    }
    
    @ViewBuilder
    private var page: some View{
        switch viewModel.route{
        case .Dashboard:
            DashboardPageView()
        case .Examination:
            ExaminationPageView()
        case .Exam(let exam_id):
            LiveExaminationPageView(exam_id: exam_id)
//        case .Settings:
//            SettingsPageView()
        case .Profile:
            ProfilePageView()
        }
    }
}

struct ApplicationContainerView_Previews: PreviewProvider {
    static var previews: some View {
        ApplicationContainerView()
            .environmentObject(ApplicationContainerViewModel())
    }
}
