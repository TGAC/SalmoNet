// Gruntfile.js

module.exports = function(grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        sass: {
			dist: {
				files: {
					'src/css/style.css' : 'src/sass/style.scss'
                }
			}
		},
        cssmin: {
            options: {
                shorthandCompacting: false,
                roundingPrecision: -1
            },
            dist: {
                files: {
                    'dist/css/style.css': ['src/css/*.css', 'template/node_modules/webix/webix.css']
                }
            }
        },
        uglify: {  
            options: {
                compress: true  
            },  
            dist: {
                src: [
                    'node_modules/uikit/src/js/components/sticky.js',
                    'node_modules/uikit/src/js/core/*.js',
                    'node_modules/jquery/dist/jquery.js',
                    'node_modules/webix/webix.js',
                    'src/js/*.js'
                ],  
                dest: 'dist/js/app.js'
            }  
        },
        processhtml: {
            dist: {
                files: {
                    'dist/index.html': ['src/index.html'],
                    'dist/browse.html': ['src/browse.html'],
                    'dist/download.html': ['src/download.html']
                }
            }
        },
		watch: {
			sass: {
				files: 'src/sass/*.scss',
				tasks: ['sass']
			},
			css: {
				files: 'src/css/*.css',
				tasks: ['cssmin']
			},
			js: {
				files: 'src/js/*.js',
				tasks: ['uglify']
			},
			html: {
				files: 'src/*.html',
				tasks: ['processhtml']
			}
		},
        clean: {
            dist: ['dist']
        }
    });

    grunt.loadNpmTasks('grunt-processhtml');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-clean');
    
    grunt.registerTask('build',['sass', 'cssmin', 'uglify', 'processhtml']);
    grunt.registerTask('default',['build']);
};