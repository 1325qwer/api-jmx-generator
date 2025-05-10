from jinja2 import Environment, FileSystemLoader
import os

def generate_jmx(apis, output_path="output/output_test.jmx"):
    # 初始化 Jinja2 模板环境
    env = Environment(
        loader=FileSystemLoader("app/templates"),
        trim_blocks=True,
        lstrip_blocks=True
    )
    template = env.get_template("http_sampler.xml")

    # 渲染每个接口
    samplers = []
    for api in apis:
        rendered = template.render(**api)
        samplers.append(rendered)

    # 🔧 正确拼接：模板中每个 sampler 已含 hashTree，这里无需手动加 <hashTree/>
    sampler_block = "\n".join(samplers)

    # 构造完整 .jmx 文件
    full_jmx = f"""<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2" properties="5.0" jmeter="5.4.1">
  <hashTree>
    <TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="自动生成计划" enabled="true">
      <stringProp name="TestPlan.comments"/>
      <boolProp name="TestPlan.functional_mode">false</boolProp>
      <boolProp name="TestPlan.serialize_threadgroups">false</boolProp>
      <elementProp name="TestPlan.user_defined_variables" elementType="Arguments">
        <collectionProp name="Arguments.arguments"/>
      </elementProp>
      <stringProp name="TestPlan.user_define_classpath"/>
    </TestPlan>
    <hashTree>
      <ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="线程组" enabled="true">
        <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
        <elementProp name="ThreadGroup.main_controller" elementType="LoopController" guiclass="LoopControlPanel" testclass="LoopController" testname="循环控制器" enabled="true">
          <boolProp name="LoopController.continue_forever">false</boolProp>
          <stringProp name="LoopController.loops">1</stringProp>
        </elementProp>
        <stringProp name="ThreadGroup.num_threads">1</stringProp>
        <stringProp name="ThreadGroup.ramp_time">1</stringProp>
        <stringProp name="ThreadGroup.delay">0</stringProp>
        <stringProp name="ThreadGroup.duration"/>
        <boolProp name="ThreadGroup.scheduler">false</boolProp>
        <boolProp name="ThreadGroup.same_user_on_next_iteration">true</boolProp>
      </ThreadGroup>
      <hashTree>
        {sampler_block}
      </hashTree>
    </hashTree>
  </hashTree>
</jmeterTestPlan>
"""

    # 写入 JMX 文件
    os.makedirs("output", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_jmx)

    return output_path
