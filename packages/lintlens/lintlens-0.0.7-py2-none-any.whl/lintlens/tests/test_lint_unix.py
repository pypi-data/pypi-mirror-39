from ..lint.unix import parse_report, LintEntry

raw_report = """\
/var/lib/jenkins/workspace/Example project/components/DropdownMenu.jsx:6:1: Component should be written as a pure function [Error/react/prefer-stateless-function]
/var/lib/jenkins/workspace/Example project/components/DropdownMenu.jsx:26:3: Prop type `object` is forbidden [Error/react/forbid-prop-types]
/var/lib/jenkins/workspace/Example project/components/DropdownMenu.jsx:73:7: Do not use setState in componentDidUpdate [Error/react/no-did-update-set-state]
/var/lib/jenkins/workspace/Example project/components/DropdownMenu.jsx:112:28: Unexpected usage of singlequote. [Warning/jsx-quotes]
/var/lib/jenkins/workspace/Example project/index.js:2:8: 'jquery' is defined but never used. [Warning/no-unused-vars]
/var/lib/jenkins/workspace/Example project/package/utils.js:1:15: Strings must use singlequote. [Warning/quotes]
/var/lib/jenkins/workspace/Example project/package/utils.js:2:15: Strings must use singlequote. [Warning/quotes]
/var/lib/jenkins/workspace/Example project/package/utils.js:4:1: Prefer default export. [Warning/import/prefer-default-export]
/var/lib/jenkins/workspace/Example project/package/utils.js:4:14: Identifier 'package_utils' is not in camel case. [Warning/camelcase]
/var/lib/jenkins/workspace/Example project/package/utils.js:5:1: Expected indentation of 2 spaces but found 4. [Error/indent]
"""


def test_parse_report_parses_raw_report():
    report = parse_report(raw_report)
    assert len(report) == 10
    assert all((isinstance(item, LintEntry)) for item in report)
