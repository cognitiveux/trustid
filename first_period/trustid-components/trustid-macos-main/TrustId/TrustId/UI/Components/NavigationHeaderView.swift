//
//  NavigationHeaderView.swift
//  TrustId
//
//  Created by Adamos Adamou on 30/11/21.
//

import SwiftUI

struct NavigationHeaderView: View {
    
    @EnvironmentObject var applicationViewModel:ApplicationContainerViewModel
    
    @StateObject var viewModel = NavigationHeaderViewModel()
    
    var showOnlyLogo = false
    
    var userService = UserService.shared
    
    private let buttonFactory = NavigationHeaderButtonConfigurationFactory()
    
    var body: some View {
        HStack{
            Image("trustid-id")
                .resizable()
                .aspectRatio(nil, contentMode: .fit)
                .frame(height:55-24)
            Spacer()
            if !showOnlyLogo{
                menuView
                Spacer()
                profileView
            }
        }
        .padding(16)
        .background(TrustIdPalette.lightGray)
    }
    
    private var menuView:some View{
        HStack(spacing:64){
            NavigationHeaderButton(configuration: buttonFactory.makeDashboard())
                .onTapGesture(perform: viewModel.tappedDashboard)
                .foregroundColor(foregroundColorForRoute(.Dashboard))
            
            NavigationHeaderButton(configuration: buttonFactory.makeExaminations())
                .onTapGesture(perform: viewModel.tappedExaminations)
                .foregroundColor(foregroundColorForRoute(.Examination))
            
//            NavigationHeaderButton(configuration: buttonFactory.makeSettings())
//                .onTapGesture(perform: viewModel.tappedSettings)
//                .foregroundColor(foregroundColorForRoute(.Settings))
        }
    }
    
    private var profileView:some View{
        
        let backgroundColor = applicationViewModel.route == .Profile
            ? TrustIdPalette.buttonBlue
            : TrustIdPalette.profileBlue
        
        return Text(userService.retrieveUser()?.initials ?? "-")
            .font(.custom("Roboto", size: 13))
            .padding(8)
            .background(backgroundColor)
            .foregroundColor(.white)
            .clipShape(RoundedRectangle.init(cornerRadius: 8))
            .onTapGesture(perform: viewModel.tappedProfile)
    }
    
    private func foregroundColorForRoute(_ route:PageRoute) -> Color{
        return applicationViewModel.route == route
            ? TrustIdPalette.buttonBlue
            : .black
    }
}

struct NavigationHeaderView_Previews: PreviewProvider {
    static var previews: some View {
        NavigationHeaderView(showOnlyLogo: false)
            .frame(height: 55)
            .preferredColorScheme(.light)
            .environmentObject(ApplicationContainerViewModel())
    }
}
