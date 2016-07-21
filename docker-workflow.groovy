node {
    docker.withRegistry("http://127.0.0.1:5000/") {
        // Mark the code checkout 'stage'....
        stage 'Checkout'
        
        // Get some code from a GitHub repository
        git url: 'https://github.com/phinexdaz/identity_generator.git'
        
        stage 'Build Image'
        // Build image with BUILD_NUMBER
        def img = docker.build("web/identity:${env.BUILD_NUMBER}", '.')
        
        stage 'Push Image'
        // Push image to registry
        img.push()
    }
}