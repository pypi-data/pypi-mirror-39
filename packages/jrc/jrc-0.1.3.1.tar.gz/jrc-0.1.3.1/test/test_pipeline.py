import os
from jrc import Compiler
from jrc import PipelineExtension


def test_pipeline():
    dsl_str = """
    #应用名
    application: myapp
    label: myapp DevOps Go!
    language: java
    
    pipeline:
      # CI 流水线配置
      return1: 
          name: return1
          module: module1
          status: disable
          agent: master
      A010: 
          name: 代码检出
          module: Git-module-checkout
          status: enable
          gitUrl: github.com
    """
    lang_tx_str = """
    /*
        A grammar for JSON data-interchange format.
        See: http://www.json.org/
    */
    File:
        Array | Object
    ;
    
    Array:
        "[" values*=Value[','] "]"
    ;
    
    Value:
        STRING | FLOAT | BOOL | Object | Array | "null"
    ;
    
    Object:
        "{" nodes*=Member[','] "}"
    ;
    
    Member:
        key=STRING ':' value=Value
    ;
    """

    out_code = """pipeline{
    agent { node { label 'myapp DevOps Go!' } }
    stages {

    
stage('return1'){
    agent { label 'master'}
    steps{
        updateGitlabCommitStatus name: 'myapp DevOps Go!', state: 'running'
    }
}
stage('A010_代码检出') {
    agent { label ''}
    steps {
    script{
        updateGitlabCommitStatus name: 'A010_代码检出', state: 'running'
			    checkout changelog: false, poll: false, scm: [$class: 'GitSCM',  url: 'github.com']]]
            }
    }
    post {
        failure {
            updateGitlabCommitStatus name: 'myapp DevOps Go!', state: 'failed'
            updateGitlabCommitStatus name: 'checkout', state: 'failed'
        }
        success {
            updateGitlabCommitStatus name: 'A010_代码检出', state: 'success'
            echo "OK"
        }
        aborted {
            echo "Skip"
        }
    }
}

    }
}"""
    my_path = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(my_path, '../demo/pipeline/template/')
    params = {
        'dsl_str': dsl_str,
        'lang_tx_str': lang_tx_str,
        'template_path': template_path,
        'extension':  PipelineExtension(template_path=template_path)
    }
    my_parser = Compiler(**params)
    my_parser.compile()
    assert my_parser.out_code == out_code
