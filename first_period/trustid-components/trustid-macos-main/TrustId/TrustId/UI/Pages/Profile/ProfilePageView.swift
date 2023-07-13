//
//  ProfilePageView.swift
//  TrustId
//
//  Created by Adamos Adamou on 6/12/21.
//

import SwiftUI

struct ProfilePageView: View {
    
    @StateObject private var viewModel = ProfilePageViewModel()
    
    var body: some View {
        VStack {
            HStack(spacing:64){
                Image(systemName: "person.fill")
                    .resizable()
                    .frame(width: 70, height: 70)
                
                VStack(alignment:.leading, spacing: 16){
                    Text(viewModel.user.fullName)
                        .font(.custom("Roboto", size: 13))
                    Text(userType)
                        .font(.custom("Roboto", size: 13))
                }
                
                Spacer()
                
                Button("Logout"){
                    viewModel.logout()
                }
                .font(.custom("Roboto", size: 13))
                .buttonStyle(BlueButton())
            }
            Spacer()
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .padding()
        .background(Color.white)
        .addNavigationHeader()
    }
    
    private var userType:String{
        switch viewModel.user.type{
        case .student: return "Student"
        case .instructor: return "Instructor"
        }
    }
}

struct ProfilePageView_Previews: PreviewProvider {
    static var previews: some View {
        ProfilePageView()
            .preferredColorScheme(.light)
    }
}
